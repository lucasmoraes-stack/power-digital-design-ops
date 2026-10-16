const imgPhotoCard = "assets/a4067dca-07bc-4d8c-823d-66afa7eee643.png";
const imgVector12 = "assets/455a5377-a650-4526-9b93-e09331a5d046.svg";
const imgKatapultLogoWhite = "assets/ceebe240-ab2a-4cf6-afe3-ad30699329b8.svg";

export default function Template06TopBlockRoundedCard16X9() {
  return (
    <div className="bg-[#ed5370] relative size-full" data-node-id="547:1265" data-name="template-06-top-block-rounded-card-16x9">
      <div className="absolute h-[1262.636px] left-[-457px] mix-blend-soft-light top-[605px] w-[2429.41px]" data-node-id="547:1266">
        <div className="absolute inset-[-9.64%_-1.42%_-9.64%_0]">
          <img alt="" className="block max-w-none size-full" src={imgVector12} />
        </div>
      </div>
      <div className="absolute h-[930px] left-[calc(50%+100px)] rounded-[48px] top-[75px] w-[840px]" data-node-id="547:1267" data-name="photo-card">
        <div aria-hidden className="absolute inset-0 pointer-events-none rounded-[48px]">
          <img alt="" className="absolute max-w-none object-cover rounded-[48px] size-full" src={imgPhotoCard} />
          <div className="absolute bg-[rgba(0,0,0,0.25)] inset-0 rounded-[48px]" />
        </div>
      </div>
      <p className="-translate-x-1/2 [text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] absolute font-['Inter:Medium'] font-medium leading-[1.2] left-1/2 not-italic text-[15px] text-center text-white top-[1027px] w-[552px]" data-node-id="547:1268">
        Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.
      </p>
      <div className="-translate-x-1/2 absolute content-stretch flex flex-col gap-[48px] items-center left-[calc(25%+40px)] top-[271.19px]" data-node-id="547:1269">
        <div className="content-stretch flex items-center relative shrink-0" data-node-id="547:1270">
          <div className="h-[31.616px] relative shrink-0 w-[142px]" data-node-id="547:1271" data-name="Katapult Logo (White)">
            <img alt="" className="absolute block inset-0 max-w-none size-full" src={imgKatapultLogoWhite} />
          </div>
        </div>
        <div className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[0] not-italic relative shrink-0 text-[112px] text-center text-white tracking-[-4.48px] w-[960px]" data-node-id="547:1277">
          <p className="leading-[0.9] mb-0">Time for the home</p>
          <p className="leading-[0.9]">upgrade you want.</p>
        </div>
        <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.3] not-italic relative shrink-0 text-[40px] text-[rgba(255,255,255,0.85)] text-center w-[960px]" data-node-id="547:1278">
          No credit score needed. Just fair, straightforward terms.
        </p>
        <div className="bg-[#131540] content-stretch flex items-center justify-center overflow-clip px-[64px] py-[32px] relative rounded-[49.5px] shrink-0" data-node-id="547:1279" data-name="Button">
          <p className="[text-box-edge:cap_alphabetic] [text-box-trim:trim-both] [word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.2] not-italic relative shrink-0 text-[73.91px] text-white whitespace-nowrap" data-node-id="I547:1279;2485:67">
            Leap Forward
          </p>
        </div>
      </div>
    </div>
  );
}
